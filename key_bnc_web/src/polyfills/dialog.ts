export async function polyfillDialogIfNeeded() {
	if (typeof HTMLDialogElement == 'function') {
		return;
	}
	await Promise.allSettled([
		import('dialog-polyfill').then((val) => {
			window.dialogPolyfill = val.default
		}),
		import('dialog-polyfill/dialog-polyfill.css'),
	]);
}

export const isDialog = (item: unknown): item is HTMLDialogElement => Boolean(item)
	&& Object.hasOwnProperty.call(item, 'showModal')
	&& Object.hasOwnProperty.call(item, 'close');
