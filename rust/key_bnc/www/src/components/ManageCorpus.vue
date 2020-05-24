<template>
	<div>
		<h2>Manage Corpus</h2>
		<form ref="form">
			<input
				ref="input"
				type="file"
				multiple
				@change="onFileChange"
			/>
		</form>
		<p>{{ allFiles.length }} files loaded.</p>
		<ul class="file-list">
			<li
				v-for="f in allFiles"
				:key="f.id"
				class="file-list-item"
			>
				<span>{{ f.name }}</span>
				<button
					class="remove-button no-outline"
					@click="removeFile(f.id)"
				>
					Remove
				</button>
			</li>
		</ul>
	</div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Ref } from 'vue-property-decorator'
import { KeyBnc } from '../../../pkg/key_bnc'

interface FileObject {
	name: string;
	id: number;
}

@Component
export default class ManageCorpus extends Vue {
	@Ref() readonly form!: HTMLFormElement
	@Ref() readonly input!: HTMLInputElement
	@Prop() private keyBnc!: KeyBnc

	private allFiles: Array<FileObject> = []

	onFileChange () {
		if (this.input.files === null) {
			return
		}

		for (let i = 0; i < this.input.files.length; i++) {
			const f = this.input.files[i]
			if (f !== null) {
				this.processFile(f)
			}
		}

		this.form.reset()
	}

	processFile (f: File) {
		const fileReader = new FileReader()
		const name = f.name
		fileReader.onloadend = () => {
			const id = this.keyBnc.add_entry(fileReader)
			this.allFiles.push({
				id,
				name,
			})
		}
		fileReader.readAsText(f)
		this.$emit('corpus-changed')
	}

	removeFile (toRemove: number) {
		this.keyBnc.remove_entry(toRemove)
		this.allFiles = this.allFiles.filter(({ id }) => id !== toRemove)
	}
}
</script>

<style lang="scss" scoped>
.file-list {
	> * + * {
		margin-top: 1rem;
	}
}
.file-list-item {
	> * + * {
		margin-left: 1rem;
	}
}
.remove-button {
	border-radius: 5px;
	background-color: #eee;
	border: 2px solid #eee;
	&:hover,
	&:focus {
		border-color: #111;
	}
}
</style>
