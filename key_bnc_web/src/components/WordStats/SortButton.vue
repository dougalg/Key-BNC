<template>
	<button
		role="button"
		class="sort-button no-outline"
		:class="{
			'sort-button--active': sort !== SortDirection.NONE,
			'sort-button--asc': sort === SortDirection.ASC,
			'sort-button--desc': sort === SortDirection.DESC,
		}"
	>
		<slot />
		<svg
			class="sort-arrows"
			viewBox="0 0 18 18"
			xmlns="http://www.w3.org/2000/svg"
		>
			<path
				class="top-arrow"
				d="M9 2 L15 7 L3 7Z"
			/>
			<path
				class="bottom-arrow"
				d="M9 16 L15 11 L3 11Z"
			/>
		</svg>
	</button>
</template>

<script lang="ts">
import { defineComponent, PropType } from '@vue/runtime-core'
import { SortDirection } from '@/models'

export default defineComponent({
	props: {
		sort: {
			type: Number as PropType<SortDirection>,
			required: true,
		},
	},
	setup () {
		return {
			SortDirection,
		}
	},
})
</script>

<style lang="scss" scoped>
.sort-button {
	position: relative;
	width: 100%;
	display: flex;
	align-items: center;
	justify-content: space-between;
	font-size: 1.6rem;
	font-weight: 600;
	padding: 0.5rem 1rem;
	border-radius: 3px;
	white-space: nowrap;

	&:hover,
	&:focus {
		background-color: #ddd;
	}
}

.sort-button--active {
	border-radius: 0;
	background-color: #efefef;
	transition: border-radius 0.3s;
}

.sort-button--active::before {
	content: "";
	position: absolute;
	top: 0;
	left: 0;
	right: 0;
	border-bottom: 2px solid black;
}

.sort-arrows {
	height: 1rem;
	width: 1rem;
	margin-left: 1rem;
	fill: #aaa;
}

.sort-button--asc .top-arrow {
	fill: black;
}

.sort-button--desc .bottom-arrow {
	fill: black;
}
</style>
