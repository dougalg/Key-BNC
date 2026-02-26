<script setup lang="ts">
import { computed, ref } from 'vue'
import changelog from "virtual:changelog";
import BaseModal from '@/components/BaseModal.vue'
import BasicButton from '@/components/buttons/BasicButton.vue';
import { isOlderRelease, isVersionSameOrNewerThan } from "@/utils/version";
import ChangelogHeading from './ChangelogHeading.vue';

const STORAGE_KEY = 'bnc_acknowledged_version';
const acknowledgedVersion = ref<string | null>(localStorage.getItem(STORAGE_KEY));

const props = defineProps<{
	version: string,
	open: boolean,
}>()

const showChangelog = computed((): boolean => {
	if (acknowledgedVersion.value === props.version) return false;
	return changelog.releases.some((r) => {
		if (!r.version) return false;
		if (!acknowledgedVersion.value) return true;
		return isVersionSameOrNewerThan(r.version, acknowledgedVersion.value!);
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
	changelog.releases.filter((r) => !isOlderRelease(r, acknowledgedVersion.value)))

const showOlderReleases = ref(false);

const hasOlderReleases = computed(() =>
	changelog.releases.some((r) => isOlderRelease(r, acknowledgedVersion.value)))

const olderReleases = computed(() =>
	!showOlderReleases.value
		? []
		: changelog.releases
			.filter((r) => isOlderRelease(r, acknowledgedVersion.value)));

</script>

<template>
	<base-modal
		:open="showChangelog || props.open"
		@close="onChangelogClose"
	>
		<h2 tabindex="-1">What's new</h2>
		<div>
			<template
				v-for="release in newReleases"
				:key="release.version"
			>
				<ChangelogHeading
					:version="release.version"
					:date="release.date"
				/>
				<ul>
					<li
						v-for="(item, i) in release.items"
						:key="i"
						v-html="item"
					/>
				</ul>
			</template>
			<template
				v-for="release in olderReleases"
				:key="release.version"
			>
				<ChangelogHeading
					:version="release.version"
					:date="release.date"
				/>
				<ul>
					<li
						v-for="(item, i) in release.items"
						:key="i"
						v-html="item"
					/>
				</ul>
			</template>
		</div>
		<div class="button-wrapper">
			<basic-button @click="onChangelogClose">
				Got it
			</basic-button>
			<basic-button
				v-if="hasOlderReleases && !showOlderReleases"
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
