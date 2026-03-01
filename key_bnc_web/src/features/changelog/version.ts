export function parseVersionParts(version: string): number[] {
	return version.replace(/^[vV]/, '').split('.').map(Number)
}

export function isVersionNewerThan(candidate: string, baseline: string): boolean {
	const [cMajor, cMinor, cPatch = Infinity ] = parseVersionParts(candidate)
	const [bMajor, bMinor, bPatch = 0] = parseVersionParts(baseline)
	if (cMajor != bMajor) {
		return cMajor > bMajor;
	}
	if (cMinor != bMinor) {
		return cMinor > bMinor;
	}
	if (cPatch != bPatch) {
		return cPatch > bPatch;
	}
	return false;
}

export function isOlderRelease(version: string, acknowledgedVersion: string | null) {
	if (!version) return false
	if (!acknowledgedVersion) return false
	return !isVersionNewerThan(version, acknowledgedVersion || '');
}
