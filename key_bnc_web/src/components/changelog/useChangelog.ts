import { useLocalStorage } from '@vueuse/core';
import { changelog } from './changelog'

export const lastViewedVersion = useLocalStorage('LAST_VIEWED_VERSION', 'v2.4')
export const latestVersion = changelog[0].id
