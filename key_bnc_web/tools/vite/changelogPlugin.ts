import fs from "fs";
import z from 'zod';

type ChangelogRelease = z.infer<typeof changelogSchema>;

const versionRe = /^##\s+(v\d[\d.]*)/i
const itemRe = /^[-*]\s+(.+)/
const dateRe = /\d{4}/

const changelogSchema = z.object({
	version: z.string().regex(/^v\d(.\d){1,2}$/i),
	date: z.string(),
	items: z.array(z.string()),
})

function parseChangelog(raw: string): ChangelogRelease[] {
	const releases: ChangelogRelease[] = []
	let current: ChangelogRelease | null = null
	let expectDate = false

	for (const rawLine of raw.split('\n')) {
		const line = rawLine.trim()

		const versionMatch = line.match(versionRe)
		if (versionMatch) {
			if (current) {
				changelogSchema.parse(current)
				releases.push(current)
			}

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

	if (current) {
		changelogSchema.parse(current)

		releases.push(current)
	}
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
