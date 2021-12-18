import { isDialog } from '@/polyfills/dialog';
import { MaybeElementRef, unrefElement } from '@vueuse/core';
import { isRef, ref, watch } from 'vue-demi';

export interface UseDialog {
	open(): void;
	close(): void;
}

export const useDialog = (
	dialog: MaybeElementRef,
) => {
	const isOpen = ref(false);
	const open = () => {
		const val = unrefElement(dialog);
		isOpen.value = true;
		if (!isDialog(val)) {
			return;
		}
		val.showModal();
	};
	const close = () => {
		const val = unrefElement(dialog);
		isOpen.value = false;
		if (!isDialog(val)) {
			return;
		}
		try {
			val.close();
		} catch(e) {}
	};

	if (isRef(dialog)) {
		watch(dialog, () => {
			const curr = unrefElement(dialog);
			if (!curr) {
				return;
			}
			if (window.dialogPolyfill) {
				window.dialogPolyfill.registerDialog(curr as HTMLDialogElement);
			}
			if (isOpen.value) {
				open();
			} else {
				close();
			}
		}, { immediate: true });
	}

	return { open, close, isOpen };
};
