export interface WordStats {
	word: string;
	frequency: number;
	frequency_bnc: number;
	log_likelyhood: number;
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
