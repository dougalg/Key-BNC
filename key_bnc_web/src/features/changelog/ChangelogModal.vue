<script setup lang="ts">
import { computed, ref } from 'vue'
import changelogData from "virtual:changelog";
import BaseModal from '@/components/BaseModal.vue'
import BasicButton from '@/components/buttons/BasicButton.vue';
import ChangelogHeading from './ChangelogHeading.vue';
import { useChangelog } from './useChangelog';

const props = defineProps<{
	version: string,
	open: boolean,
}>()

const { newReleases, ...changelog } = useChangelog(changelogData, props.version);

const showChangelog = computed((): boolean => props.open || newReleases.value.length > 0);

const onChangelogClose = () => {
	changelog.acknowledgeLatestVersion();
	showOlderReleases.value = false;
	emit('close')
};

const emit = defineEmits<{
	(e: 'close'): void
}>()

const showOlderReleases = ref(false);

const hasOlderReleases = computed(() => changelog.olderReleases.value.length > 0)

const olderReleases = computed(() =>
	!showOlderReleases.value
		? []
		: changelog.olderReleases.value);

</script>

<template>
	<base-modal
		:open="showChangelog"
		@close="onChangelogClose"
	>
		<h2 tabindex="-1">
			What's new
		</h2>
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
