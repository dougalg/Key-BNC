import { WordStats } from '@/models'

export const WORD_STAT_HEADERS = {
	word: 'Word Type',
	frequency: 'Frequency',
	// eslint-disable-next-line @typescript-eslint/camelcase
	frequency_bnc: 'Frequency BNC',
	// eslint-disable-next-line @typescript-eslint/camelcase
	log_likelihood: 'Log-Likelihood',
	// eslint-disable-next-line @typescript-eslint/camelcase
	odds_ratio: 'Odds Ratio',
	dispersion: 'Dispersion',
} as Record<keyof WordStats, string>
