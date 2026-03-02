import { computed, ref } from 'vue'
import { Changelog, ChangelogRelease } from '@/typings/changelog'
import { isOlderRelease } from './version'

const STORAGE_KEY = 'bnc_acknowledged_version'

export function useChangelog(changelog: Changelog, appVersion: string) {
	const acknowledgedVersion = ref<string | null>(localStorage.getItem(STORAGE_KEY))

	const newReleases = computed((): ChangelogRelease[] =>
		changelog.releases.filter((r) => !isOlderRelease(r.version, acknowledgedVersion.value)),
	);

	const olderReleases = computed((): ChangelogRelease[] =>
		changelog.releases.filter((r) => isOlderRelease(r.version, acknowledgedVersion.value)),
	);

	function acknowledgeLatestVersion() {
		localStorage.setItem(STORAGE_KEY, appVersion)
		acknowledgedVersion.value = appVersion
	}

	return { newReleases, olderReleases, acknowledgeLatestVersion }
}
