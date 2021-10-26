<template>
	<button
		role="tab"
		type="button"
		class="nav-tab no-outline"
		:aria-selected="isSelected"
		:class="{
			'is-selected': isSelected,
		}"
	>
		<slot />
	</button>
</template>

<script lang="ts">
import { defineComponent } from '@vue/runtime-core'

export default defineComponent({
	props: {
		isSelected: Boolean,
	},
})
</script>

<style lang="scss" scoped>
.nav-tab {
	position: relative;
	background: white;
	border-top-left-radius: 3px;
	border-top-right-radius: 3px;
	border-color: black;
	border-width: 1px;
	border-style: solid;
	font-weight: bold;
	font-size: 1.5rem;

	@media screen and (max-width: 740px) {
		font-size: 1.1rem;
	}

	&.is-selected {
		position: relative;
		z-index: 1;
		border-bottom-color: white;
	}

	&:hover,
	&:focus {
		background-color: #eee;
		border-bottom-color: #eee;

		&::after {
			content: "";
			position: absolute;
			bottom: -3px;
			left: 0;
			width: 100%;
			border-bottom: 3px solid black;
		}
	}
}

.nav-tab + .nav-tab {
	margin-left: 1rem;
}
</style>
