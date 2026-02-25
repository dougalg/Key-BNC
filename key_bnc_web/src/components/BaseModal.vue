<script setup lang="ts">
import { onMounted, ref, watchEffect } from 'vue'

const dialog = ref<HTMLDialogElement | undefined | null>(null);
const internalOpen = ref(false);

const props = defineProps<{
	open: boolean
}>()

const emit = defineEmits<{
	(e: 'close'): void
}>()

function showHideDialog() {
	if (!dialog?.value) return;
	if (props.open) dialog.value.showModal();
	else dialog.value.close();
}

onMounted(() => {
	watchEffect(() => {
		if (props.open !== internalOpen.value) {
			showHideDialog();
			internalOpen.value = props.open;
		}
	});
});
</script>

<template>
	<dialog
		ref="dialog"
		@close="emit('close')"
	>
		<slot />
	</dialog>
</template>

<style scoped>
dialog {
	border-radius: 5px;
}
</style>
