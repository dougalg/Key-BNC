<template>
	<button
		class="basic-button no-outline"
		:class="{
			'basic-button--is-attached': isAttached,
		}"
	>
		<slot />
	</button>
</template>

<script lang="ts">
import { defineComponent } from '@vue/runtime-core'

export default defineComponent({
	props: {
		isAttached: Boolean,
	},
})
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
