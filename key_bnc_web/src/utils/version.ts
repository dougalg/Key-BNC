import { ChangelogRelease } from "@/typings/changelog"

export function parseVersionParts(version: string): number[] {
	return version.replace(/^[vV]/, '').split('.').map(Number)
}

export function isVersionSameOrNewerThan(candidate: string, baseline: string): boolean {
	const ca = parseVersionParts(candidate)
	const ba = parseVersionParts(baseline)
	for (let i = 0; i < Math.min(ca.length, ba.length); i++) {
		const c = ca[i] ?? 0
		const b = ba[i] ?? 0
		if (c !== b) return b < c
	}
	return true
}

export function isOlderRelease(r: ChangelogRelease, acknowledgedVersion: string | null) {
	if (!r.version) return false
	if (!acknowledgedVersion) return true
	return !isVersionSameOrNewerThan(r.version, acknowledgedVersion || '');
}
