<template>
	<button
		role="tab"
		type="button"
		class="nav-tab no-outline"
		:aria-selected="isSelected.toString()"
		:class="{
			'is-selected': isSelected,
		}"
	>
		<slot />
	</button>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'

@Component
export default class NavButton extends Vue {
	@Prop() readonly isSelected!: boolean
}
</script>

<style lang="scss" scoped>
.nav-tab + .nav-tab {
	margin-left: 1rem;
}
.nav-tab {
	position: relative;
	background: white;
	border-top-left-radius: 3px;
	border-top-right-radius: 3px;
	border-color: black;
	border-width: 1px;
	border-style: solid;

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
			content: '';
			position: absolute;
			bottom: -3px;
			left: 0;
			width: 100%;
			border-bottom: 3px solid black;
		}
	}
}
</style>
