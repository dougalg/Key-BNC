<template>
	<button
		class="basic-button no-outline"
		:class="{
			'basic-button--is-attached': isAttached,
		}"
		@click="$emit('click')"
	>
		<slot />
	</button>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'

@Component
export default class BasicButton extends Vue {
	@Prop(Boolean) isAttached!: boolean;
}
</script>

<style lang="scss">
.basic-button {
	border-radius: 5px;
	background-color: #eee;
	border: 2px solid #eee;
	&:hover,
	&:focus {
		border-color: #111;
	}
}

.basic-button--is-attached {
	border-radius: 5px 0 0 5px;
}

.basic-button--is-attached + .basic-button--is-attached {
	border-radius: 0 5px 5px 0;
}
</style>
