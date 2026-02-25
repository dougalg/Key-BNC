export function parseVersionParts(version: string): number[] {
	return version.replace(/^[vV]/, '').split('.').map(Number)
}

export function isVersionNewerThan(candidate: string, baseline: string): boolean {
	const ca = parseVersionParts(candidate)
	const ba = parseVersionParts(baseline)
	for (let i = 0; i < Math.max(ca.length, ba.length); i++) {
		const c = ca[i] ?? 0
		const b = ba[i] ?? 0
		if (c !== b) return c > b
	}
	return false
}

export function isCleanVersion(v: string): boolean {
	return /^[vV]?\d+(\.\d+)*$/.test(v)
}
