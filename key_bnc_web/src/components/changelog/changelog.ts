export interface Release {
	id: string;
	releaseDate: Date;
	features: Change[];
}

export interface Change {
	description: string;
	type: ChangeType;
}

export enum ChangeType {
	BUG,
	FEATURE,
	BREAKING_FEATURE,
}

export const changelog: Release[] = [
	{
		id: "v2.5",
		releaseDate: new Date("2021-10-26"),
		features: [
			{
				description: "Notify users of new features when they are available.",
				type: ChangeType.FEATURE,
			},
			{
				description: "Add support for PDF files",
				type: ChangeType.FEATURE,
			},
		],
	},
	{
		id: "v2.4",
		releaseDate: new Date("2021-09-21"),
		features: [
			{
				description: "Add PanelBear analytics (no tracking data).",
				type: ChangeType.FEATURE,
			},
		],
	},
	{
		id: "v2.3",
		releaseDate: new Date("2021-07-18"),
		features: [
			{
				description: "Add CSV downloads.",
				type: ChangeType.FEATURE,
			},
			{
				description: "Add new logo.",
				type: ChangeType.FEATURE,
			},
		],
	},
]
