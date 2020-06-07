<template>
	<div class="stats-filters dropdown-wrapper">
		<div
			class="button-wrapper"
			:class="{
				'dropdown-wrapper--active': isOpen,
			}"
		>
			<slot name="button">
				<basic-button @click="$emit('toggle')">
					<slot name="button-content" />
				</basic-button>
			</slot>
		</div>
		<div
			v-if="isOpen"
			class="dropdown-content"
		>
			<slot name="dropdown-content" />
		</div>
	</div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator'
import BasicButton from '@/components/buttons/BasicButton.vue'

@Component({ components: { BasicButton } })
export default class Dropdown extends Vue {
	@Prop() isOpen!: boolean;
}
</script>

<style lang="scss" scoped>
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

	display: flex;
	flex-direction: column;

	border-radius: 5px;
	border: 1px solid black;
	padding: 0.6rem;
	background-color: white;
}

.dropdown-content > * + * {
	margin-top: 0.5em;
}
</style>
