import { WordStats } from '@/models'

export const WORD_STAT_HEADERS = {
	word: 'Word Type',
	frequency: 'Frequency',
	frequency_bnc: 'Frequency BNC',
	log_likelihood: 'Log-Likelihood',
	odds_ratio: 'Odds Ratio',
	dispersion: 'Dispersion',
} as Record<keyof WordStats, string>
