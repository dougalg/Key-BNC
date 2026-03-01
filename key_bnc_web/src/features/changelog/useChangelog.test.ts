import { describe, it, expect, beforeEach, vi } from 'vitest'
import { useChangelog } from './useChangelog'
import { Changelog } from '@/typings/changelog'

const changelog: Changelog = {
	releases: [
		{ version: '2.0.0', date: 'Jan 1st, 2026', items: ['New feature'] },
		{ version: '1.0.0', date: 'Jan 1st, 2025', items: ['Initial release'] },
	],
}

describe('useChangelog', () => {
	beforeEach(() => {
		localStorage.clear()
	})
	describe('newReleases', () => {
		it('returns all releases when nothing has been acknowledged', () => {
			const { newReleases } = useChangelog(changelog, '2.0.0')
			expect(newReleases.value).toEqual(changelog.releases)
		})

		it('returns only releases newer than the acknowledged version', () => {
			localStorage.setItem('bnc_acknowledged_version', '1.0.0')
			const { newReleases } = useChangelog(changelog, '2.0.0')
			expect(newReleases.value).toEqual([{ version: '2.0.0', date: 'Jan 1st, 2026', items: ['New feature'] }])
		})

		it('returns no releases when the current version is already acknowledged', () => {
			localStorage.setItem('bnc_acknowledged_version', '2.0.0')
			const { newReleases } = useChangelog(changelog, '2.0.0')
			expect(newReleases.value).toEqual([])
		})

		it('updates after acknowledgeLatestVersion is called', () => {
			const { newReleases, acknowledgeLatestVersion } = useChangelog(changelog, '2.0.0')
			expect(newReleases.value).toHaveLength(2)
			acknowledgeLatestVersion()
			expect(newReleases.value).toHaveLength(0)
		})
	})

	describe('olderReleases', () => {
		it('returns no releases when nothing has been acknowledged', () => {
			const { olderReleases } = useChangelog(changelog, '2.0.0')
			expect(olderReleases.value).toEqual([])
		})

		it('returns releases older than the acknowledged version', () => {
			localStorage.setItem('bnc_acknowledged_version', '2.0.0')
			const { olderReleases } = useChangelog(changelog, '2.0.0')
			expect(olderReleases.value).toEqual(changelog.releases)
		})

		it('updates after acknowledgeLatestVersion is called', () => {
			localStorage.setItem('bnc_acknowledged_version', '1.0.0')
			const { olderReleases, acknowledgeLatestVersion } = useChangelog(changelog, '2.0.0')
			expect(olderReleases.value).toEqual([{ version: '1.0.0', date: 'Jan 1st, 2025', items: ['Initial release'] }])
			acknowledgeLatestVersion()
			expect(olderReleases.value).toEqual(changelog.releases)
		})
	})

	describe('acknowledgeLatestVersion', () => {
		it('persists the app version to localStorage', () => {
			const { acknowledgeLatestVersion } = useChangelog(changelog, '2.0.0')
			acknowledgeLatestVersion()
			expect(localStorage.getItem('bnc_acknowledged_version')).toBe('2.0.0')
		})
	})
})
