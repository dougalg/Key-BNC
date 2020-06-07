<template>
	<div>
		<h2>Manage Corpus</h2>
		<form ref="form">
			<input
				ref="input"
				type="file"
				class="file-input"
				id="fileinput"
				multiple
				@change="onFileChange"
			/>
			<label
				for="fileinput"
				class="no-outline"
			>
				Add files
			</label>
		</form>
		<p>{{ allFiles.length }} files loaded.</p>
		<ul class="file-list">
			<li
				v-for="f in allFiles"
				:key="f.id"
				class="file-list-item"
			>
				<span>{{ f.name }}</span>
				<basic-button @click="removeFile(f.id)">
					Remove
				</basic-button>
			</li>
		</ul>
	</div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Ref } from 'vue-property-decorator'
import { KeyBnc } from '../../../pkg/key_bnc'
import BasicButton from './buttons/BasicButton.vue'

interface FileObject {
	name: string;
	id: number;
}

@Component({ components: { BasicButton } })
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
		this.$emit('corpus-changed')
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

[type="file"] {
	border: 0;
	clip: rect(0, 0, 0, 0);
	height: 1px;
	overflow: hidden;
	padding: 0;
	position: absolute !important;
	white-space: nowrap;
	width: 1px;
}

[type="file"] + label {
	background-color: #000;
	border-radius: 5px;
	color: #fff;
	cursor: pointer;
	display: inline-block;
	font-family: 'Poppins', sans-serif;
	font-size: 1rem;
	font-weight: 700;
	height: 4rem;
	line-height: 4rem;
	padding-left: 2rem;
	padding-right: 2rem;
	transition: background-color 0.3s;
	border: 2px solid black;
}

[type="file"]:focus + label,
[type="file"] + label:hover {
	background-color: white;
	color: black;
}

[type="file"]:focus + label {
	outline: 1px dotted #000;
	outline: -webkit-focus-ring-color auto 5px;
}
</style>
