declare module '*.vue' {
	import Vue from 'vue'
	export default Vue
}

declare module '*.csv' {
	const content: string
	export default content
}
