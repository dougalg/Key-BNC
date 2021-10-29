<template>
	<section>
		<div class="header">
			<h3>
				{{ release.id }}
			</h3>
			<time
				:datetime="release.releaseDate.toISOString()"
			>
				{{ formattedDate }}
			</time>
		</div>
		<ul>
			<li
				v-for="({ description, type }, idx) in release.features"
				:key="idx"
			>
				{{ description }} ({{ TYPE_BADGE_TEXT[type] }})
			</li>
		</ul>
	</section>
</template>

<script setup lang="ts">
import { computed, PropType } from 'vue-demi';
import { ChangeType, Release } from './changelog';

const props = defineProps({
	release: {
		type: Object as PropType<Release>,
		required: true,
	},
})

const formatter = new Intl.DateTimeFormat('en-CA', {
	dateStyle: 'long'
})

const formattedDate = computed(() => formatter.format(props.release.releaseDate))

const TYPE_BADGE_TEXT = {
	[ChangeType.BREAKING_FEATURE]: 'Breaking Feature',
	[ChangeType.FEATURE]: 'New Feature',
	[ChangeType.BUG]: 'Bug Fix',
};
</script>
