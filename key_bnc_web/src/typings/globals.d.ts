// typings.d.ts
declare const __APP_VERSION__: string;
// eslint-disable-next-line @typescript-eslint/ban-types
interface HTMLDialogElement extends HTMLDialogElement {
	showModal(): void;
	close(): void;
}
declare const HTMLDialogElement: HTMLDialogElement | undefined;

interface DialogPolyFill {
	registerDialog(el: HTMLDialogElement): void;
}

declare interface Window {
	dialogPolyfill: DialogPolyFill;
}
