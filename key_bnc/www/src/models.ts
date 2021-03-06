export interface WordStats {
	word: string;
	frequency: number;
	frequency_bnc: number;
	log_likelihood: number;
	odds_ratio: number;
	dispersion: number;
}

export enum SortBy {
	FREQUENCY,
	FREQUENCY_BNC,
	LL,
	OR,
	DISPERSION,
}

export enum SortDirection {
	ASC,
	DESC,
	NONE,
}

export enum FilterType {
	FREQUENCY = 'frequency',
	FREQUENCY_BNC = 'frequency_bnc',
	LL = 'log_likelihood',
	OR = 'odds_ratio',
	DISPERSION = 'dispersion',
}
