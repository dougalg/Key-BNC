import { WordStats } from '@/models'
import { WORD_STAT_HEADERS } from '@/lang/wordStats'

const ORDERED_FIELDS = [
	'word',
	'frequency',
	'frequency_bnc',
	'log_likelihood',
	'odds_ratio',
	'dispersion',
] as (keyof WordStats)[]

const CSV_HEADER_STRING = ORDERED_FIELDS
	.map((f) => WORD_STAT_HEADERS[f]).join(',')

function csvEscape (val: string): string {
	return `"${val.replace('"', '""')}"`
}

export function toCSV (allStats: WordStats[]): string {
	const csvStats = allStats.map((stats) => ORDERED_FIELDS
		.map((f) => csvEscape((stats[f] || 0).toString())).join(','))
		.join('\n')
	return CSV_HEADER_STRING + '\n' + csvStats
}
