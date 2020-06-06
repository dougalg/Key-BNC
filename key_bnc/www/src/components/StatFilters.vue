<template>
	<div class="stats-filters dropdown-wrapper">
		<basic-button
			:class="{
				'dropdown-wrapper--active': isDropdownOpen,
			}"
			@click="isDropdownOpen = !isDropdownOpen"
		>
			Add Filter +
		</basic-button>
		<div
			v-if="isDropdownOpen"
			class="dropdown-content"
		>
			<basic-button @click="addFrequencyFilter">
				Frequency
			</basic-button>
		</div>
	</div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import BasicButton from './BasicButton.vue'

@Component({ components: { BasicButton } })
export default class StatFilers extends Vue {
	isDropdownOpen = false
}
</script>

<style lang="scss">
.dropdown-wrapper {
	position: relative;
}

.dropdown-wrapper--active::after {
	content: ' ';
	display: block;
	width: 1rem;
	height: 1rem;
	border-top: 1px solid black;
	border-right: 1px solid black;
	transform: translateX(-50%) rotate(-45deg);
	position: absolute;
	top: calc(100% + 5px);
	left: 50%;
	background-color: white;
	z-index: 2;
}

.dropdown-content {
	position: absolute;
	top: 100%;
	right: 0;
	z-index: 1;
	margin-top: 1rem;

	border-radius: 5px;
	border: 1px solid black;
	padding: 0.6rem;
	background-color: white;
}
</style>
