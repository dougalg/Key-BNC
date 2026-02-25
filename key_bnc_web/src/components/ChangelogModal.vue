<script setup lang="ts">
import { computed, ref } from 'vue'
import BaseModal from '@/components/BaseModal.vue'
import BasicButton from './buttons/BasicButton.vue';
import changelog from "virtual:changelog";
import { isCleanVersion, isVersionNewerThan } from "@/utils/version";

const STORAGE_KEY = 'bnc_acknowledged_version';
const acknowledgedVersion = ref<string | null>(localStorage.getItem(STORAGE_KEY));

const props = defineProps<{
	version: string,
	open: boolean,
}>()

const showChangelog = computed((): boolean => {
	if (!isCleanVersion(props.version)) return false;
	if (acknowledgedVersion.value === props.version) return false;
	return changelog.releases.some((r) => {
		if (!r.version) return false;
		if (!acknowledgedVersion.value) return true;
		return isVersionNewerThan(r.version, acknowledgedVersion.value!);
	});
});

const onChangelogClose = () => {
	localStorage.setItem(STORAGE_KEY, props.version);
	acknowledgedVersion.value = props.version;
	showOlderReleases.value = false;
	emit('close')
};

const emit = defineEmits<{
	(e: 'close'): void
}>()


const newReleases = computed(() =>
	changelog.releases.filter((r) => {
		if (!r.version) return false
		if (!acknowledgedVersion) return true
		return isVersionNewerThan(r.version, acknowledgedVersion.value || '')
	})
)

const showOlderReleases = ref(false);

const olderReleases = computed(() =>
	changelog.releases.filter((r) => {
		if (!r.version) return false
		if (!acknowledgedVersion) return true
		return !isVersionNewerThan(r.version, acknowledgedVersion.value || '')
	}))

</script>

<template>
	<base-modal
		:open="showChangelog || props.open"
		@close="onChangelogClose"
	>
		<h2>What's new</h2>
		<div>
			<template
				v-for="release in newReleases"
				:key="release.version"
			>
				<h3>
					{{ release.version }}
					<span v-if="release.date" v-html="release.date"/>
				</h3>
				<ul>
					<li
						v-for="(item, i) in release.items"
						:key="i"
					>
						{{ item }}
					</li>
				</ul>
			</template>
			<template
				v-if="showOlderReleases"
				v-for="release in olderReleases"
				:key="release.version"
			>
				<h3>
					{{ release.version }}
					<span v-if="release.date">— {{ release.date }}</span>
				</h3>
				<ul>
					<li
						v-for="(item, i) in release.items"
						:key="i"
					>
						{{ item }}
					</li>
				</ul>
			</template>
		</div>
		<div class="button-wrapper">
			<basic-button @click="emit('close')">
				Got it
			</basic-button>
			<basic-button
				v-if="olderReleases.length > 0 && !showOlderReleases"
				@click="showOlderReleases = true"
			>
				View all changes
			</basic-button>
		</div>
	</base-modal>
</template>

<style scoped>
.button-wrapper {
	display: flex;
	gap: 1rem;
}
</style>
