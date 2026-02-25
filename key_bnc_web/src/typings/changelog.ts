export interface ChangelogRelease {
	version: string // e.g. "V2.5"
	date: string // freeform e.g. "Feb 26th, 2026"; empty string if not found
	items: string[] // flat list of bullet items
}

export interface Changelog {
	releases: ChangelogRelease[]
}
