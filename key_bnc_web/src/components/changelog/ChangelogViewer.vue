<template>
	<dialog
		:id="id"
		ref="modalContent"
		class="changelog"
		aria-labelledby="dialog__label"
		aria-describedby="dialog__description"
	>
		<basic-button
			class="close-button"
			@click="updateLastViewedVersion"
		>
			Close
		</basic-button>
		<h2 id="dialog__label">
			Updates
		</h2>

		<p
			v-if="hasMultipleNewVersions"
			id="dialog__description"
		>
			{{ lastViewedReleaseIndex }} new release(s) since your last visit.
		</p>
		<p
			v-else-if="hasNoNewVersions"
			id="dialog__description"
		>
			No new updates since your last visit
		</p>

		<single-release
			v-for="release in visibleReleases"
			:key="release.id"
			:release="release"
		/>

		<basic-button
			v-if="!state.showAll && !hasNoNewVersions"
			@click="state.showAll = true"
		>
			Older Releases
		</basic-button>
	</dialog>
</template>

<script setup lang="ts">
import { changelog } from './changelog'
import { computed, reactive, ref } from 'vue'
import SingleRelease from './SingleRelease.vue'
import { lastViewedVersion, latestVersion } from './useChangelog'
import BasicButton from '../buttons/BasicButton.vue'
import { onClickOutside } from '@vueuse/core'

defineProps({
	id: {
		type: String,
		required: true,
	},
})

const emit = defineEmits(['close'])

const state = reactive({
	showAll: false,
})

const lastViewedReleaseIndex = computed(() => changelog.findIndex(({ id }) => id === lastViewedVersion.value))
const hasMultipleNewVersions = computed(() => (lastViewedReleaseIndex.value - 1) > 0);
const hasNoNewVersions = computed(() => lastViewedReleaseIndex.value === 0);

const visibleReleases = computed(() => {
	if (state.showAll || hasNoNewVersions.value) {
		return changelog
	}
	const idx = lastViewedReleaseIndex.value
	if (idx === -1) {
		return []
	}
	return changelog.slice(0, idx)
})

const updateLastViewedVersion = () => {
	lastViewedVersion.value = latestVersion
	emit('close')
}

const modalContent = ref(null)
onClickOutside(modalContent, () => {
	updateLastViewedVersion()
})
</script>

<style lang="scss" scoped>
dialog {
	position: fixed;
	top: 0;
	bottom: 0;
	right: 0;
	bottom: 0;
	overflow-y: auto;
	height: 100vh;
}

dialog::backdrop,
dialog + .backdrop {
	background: rgba(255, 255, 255, 0.8);
}

.modal {
	position: absolute;
	top: 0;
	left: 0;
	background: rgba(255, 255, 255, 0.8);
	z-index: 1;
	display: flex;
	justify-content: center;
}

.changelog {
	width: clamp(35rem, 65rem, 65rem);
	background-color: white;
	padding: 2rem 1rem;
	border: none;
	border-left: 3px solid black;
	border-right: 3px solid black;
}

.close-button {
	position: absolute;
	top: 1rem;
	right: 1rem;
}
</style>
