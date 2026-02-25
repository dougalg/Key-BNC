import fs from "fs";

interface ChangelogRelease {
	version: string
	date: string
	items: string[]
}

function parseChangelog(raw: string): ChangelogRelease[] {
	const releases: ChangelogRelease[] = []
	let current: ChangelogRelease | null = null
	let expectDate = false

	const versionRe = /^##\s+([vV]\d[\d.]*)/
	const itemRe = /^[-*]\s+(.+)/
	const dateRe = /\d{4}/

	for (const rawLine of raw.split('\n')) {
		const line = rawLine.trim()

		const versionMatch = line.match(versionRe)
		if (versionMatch) {
			if (current) releases.push(current)
			current = { version: versionMatch[1], date: '', items: [] }
			expectDate = true
			continue
		}

		if (expectDate && current && line.length > 0 && !line.startsWith('-') && !line.startsWith('*')) {
			if (dateRe.test(line)) {
				current.date = line
			}
			expectDate = false
			continue
		}

		const itemMatch = line.match(itemRe)
		if (itemMatch && current) {
			expectDate = false
			current.items.push(itemMatch[1].trim())
			continue
		}
	}

	if (current) releases.push(current)
	return releases
}

interface ChangelogPluginOptions {
	logFile: string
}

export const changelogPlugin = ({ logFile }: ChangelogPluginOptions) => {
	const virtualModuleId = 'virtual:changelog'
	const resolvedId = '\0' + virtualModuleId
	return {
		name: 'changelog-plugin',
		resolveId(id: string) {
			if (id === virtualModuleId) return resolvedId
		},
		load(id: string) {
			if (id !== resolvedId) return
			let raw: string
			try {
				raw = fs.readFileSync(logFile, 'utf-8')
			} catch {
				return `export default { releases: [] }`
			}
			return `export default ${JSON.stringify({ releases: parseChangelog(raw) })}`
		},
	}
}
