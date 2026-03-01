<script setup lang="ts">
// eslint-disable-next-line @typescript-eslint/no-unused-vars
const props = defineProps<{
	version: string,
	date?: string,
}>()
</script>

<template>
	<h3>
		{{ version }}
		<span
			v-if="date"
			v-html="date"
		/>
	</h3>
</template>
