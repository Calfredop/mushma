import { useTranslation } from 'react-i18next'
import { intlLocale, type Language } from '../i18n'
import { describeBand, OP_SYMBOL, type Trapezoid } from '../score/detail'
import type { FactorBreakdown } from '../score/impact'
import { addDays, formatDayLong, type IsoDate } from '../time/days'
import styles from './WhyBreakdown.module.css'

interface Props {
  factor: FactorBreakdown
  /** The scored day: windows and lags are counted back from it. */
  date: IsoDate
  id: string
}

const NO_BREAK_SPACE = '\u00A0'
/** Units written straight after the number: 114%, 20°. */
const TIGHT_UNITS = new Set(['%', '°'])

/**
 * What a factor measured on the scored day and what its rule wanted of it, in
 * the visitor's language. The API sends the numbers, the unit and the rule's
 * bands; this only phrases them (AGENTS.md: the model runs server-side).
 */
export function FactorDetail({ factor, date, id }: Props) {
  const { t, i18n } = useTranslation()
  const locale = intlLocale(i18n.resolvedLanguage as Language)
  const number = new Intl.NumberFormat(locale, { maximumFractionDigits: 1 })
  const list = new Intl.ListFormat(locale, { type: 'conjunction' })
  const { rule } = factor

  const quantity = (value: number, unit?: string | null, bare = false) => {
    if (unit === 'days' && !bare) return t('why.detail.days', { count: value })
    if (unit === 'growth_days' && !bare)
      return t('why.detail.growthDays', { count: value })
    if (bare || !unit) return number.format(value)
    const gap = TIGHT_UNITS.has(unit) ? '' : NO_BREAK_SPACE
    return `${number.format(value)}${gap}${unit}`
  }
  const percent = new Intl.NumberFormat(locale, {
    style: 'percent',
    maximumFractionDigits: 0,
  })

  const variableLabel = (name: string) => {
    const key = `why.detail.variable.${name}`
    return i18n.exists(key) ? t(key as 'why.detail.variable.water_balance') : name
  }
  const capitalize = (text: string) =>
    text.charAt(0).toLocaleUpperCase(locale) + text.slice(1)

  const until = (daysBefore: number) =>
    t('why.detail.until', {
      date: formatDayLong(addDays(date, -daysBefore), locale),
      lag:
        daysBefore === 0
          ? t('why.detail.sameDay')
          : t('why.detail.daysBefore', { count: daysBefore }),
    })

  type Phrasing = 'rule' | 'lag' | 'growthLag' | 'where'
  const KEYS = {
    rule: ['why.detail.rule', 'why.detail.ruleZero'],
    lag: ['why.detail.lagRule', 'why.detail.lagRuleZero'],
    growthLag: ['why.detail.growthLagRule', 'why.detail.growthLagRuleZero'],
    where: ['why.detail.where', 'why.detail.whereZero'],
  } as const

  const band = (
    trapezoid: Trapezoid,
    unit: string | null | undefined,
    phrasing: Phrasing,
    variable = '',
  ) => {
    const { full, zero } = describeBand(trapezoid)
    if (!full) return null
    const fullText = (() => {
      switch (full.kind) {
        case 'between':
          return t('why.detail.full.between', {
            from: quantity(full.from, unit, true),
            to: quantity(full.to, unit),
          })
        case 'at':
          return t('why.detail.full.at', { value: quantity(full.value, unit) })
        case 'from':
          return t('why.detail.full.from', { value: quantity(full.from, unit) })
        case 'upTo':
          return t('why.detail.full.upTo', { value: quantity(full.to, unit) })
      }
    })()
    const [withoutZero, withZero] = KEYS[phrasing]
    if (zero.length === 0) return t(withoutZero, { full: fullText, variable })
    const zeroText = list.format(
      zero.map((edge) =>
        t(`why.detail.zero.${edge.kind}` as 'why.detail.zero.below', {
          value: quantity(edge.value, unit),
        }),
      ),
    )
    return t(withZero, { full: fullText, zero: zeroText, variable })
  }

  const measurement = (): string => {
    if (!rule) return t('why.detail.none')
    if (rule.kind === 'season_window') return t('why.detail.season')
    if (rule.kind === 'habitat') return t('why.detail.habitat')
    if (factor.input == null) return t('why.detail.notMeasured')

    const offset = rule.offset_days ?? 0
    const windowEnd = offset > 0 ? until(offset) : ''
    const variable = variableLabel(rule.variable ?? '')
    switch (rule.kind) {
      case 'static_band':
        return t('why.detail.static', { value: quantity(factor.input, factor.unit) })
      case 'rain_event':
        return t('why.detail.rain', {
          count: rule.window_days ?? 0,
          amount: quantity(factor.input, factor.unit),
          until: factor.days_ago == null ? '' : until(factor.days_ago),
        })
      case 'window_aggregate':
        if ((rule.window_days ?? 0) === 1 && offset === 0) {
          return t('why.detail.windowToday', {
            variable: capitalize(variable),
            value: quantity(factor.input, factor.unit),
          })
        }
        return t('why.detail.window', {
          count: rule.window_days ?? 0,
          variable: capitalize(variable),
          aggregate: t(`why.detail.aggregate.${rule.aggregate ?? 'sum'}`),
          until: windowEnd,
          value: quantity(factor.input, factor.unit),
        })
      case 'count_days':
        return t('why.detail.count', {
          count: factor.input,
          window: number.format(rule.window_days ?? 0),
          variable,
          op: OP_SYMBOL[rule.op ?? 'gte'],
          threshold: quantity(rule.threshold ?? 0, rule.variable_unit),
          until: windowEnd,
        })
      case 'days_since':
        return t('why.detail.daysSince', {
          count: factor.input,
          variable,
          op: OP_SYMBOL[rule.op ?? 'gte'],
          threshold: quantity(rule.threshold ?? 0, rule.variable_unit),
        })
    }
  }

  /** How warmth and air humidity sped up or slowed down the growth since the rain. */
  const growth = (): string | null => {
    if (factor.input == null || factor.growth_days == null || !factor.days_ago)
      return null
    return t('why.detail.growth', {
      count: factor.days_ago,
      growth: quantity(Math.round(factor.growth_days), 'growth_days'),
      pace: percent.format(factor.growth_days / factor.days_ago),
    })
  }

  const onClock = rule?.lag_unit === 'growth_days'
  const ruleText = rule?.trapezoid ? band(rule.trapezoid, factor.unit, 'rule') : null
  const lagText = rule?.lag_days
    ? onClock
      ? band(rule.lag_days, 'growth_days', 'growthLag')
      : band(rule.lag_days, 'days', 'lag')
    : null
  const whereText = rule?.where
    ? band(
        rule.where.trapezoid,
        rule.where.variable_unit,
        'where',
        variableLabel(rule.where.variable),
      )
    : null
  const growthText = growth()

  return (
    <div id={id} className={styles.detail} data-testid="factor-detail">
      <p>{measurement()}</p>
      {growthText && <p>{growthText}</p>}
      {ruleText && <p>{ruleText}</p>}
      {lagText && <p>{lagText}</p>}
      {whereText && <p>{whereText}</p>}
    </div>
  )
}
