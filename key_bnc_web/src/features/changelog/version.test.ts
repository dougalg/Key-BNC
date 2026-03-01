import { describe, it, expect } from "vitest";
import { parseVersionParts, isVersionSameOrNewerThan, isOlderRelease } from "./version";

describe("changelog/version", () => {
	describe("parseVersionParts", () => {
		it("parses a simple version string into number parts", () => {
			expect(parseVersionParts("1.2.3")).toEqual([1, 2, 3])
		})

		it("strips a leading 'v' prefix", () => {
			expect(parseVersionParts("v1.2.3")).toEqual([1, 2, 3])
		})

		it("strips a leading 'V' prefix", () => {
			expect(parseVersionParts("V1.2.3")).toEqual([1, 2, 3])
		})

		it("parses a 2-level version into 2 parts", () => {
			expect(parseVersionParts("V1.2")).toEqual([1, 2])
		})
	})

	describe("isVersionSameOrNewerThan", () => {
		it("returns true when candidate is newer than baseline", () => {
			expect(isVersionSameOrNewerThan("2.0.0", "1.0.0")).toBe(true)
		})

		it("returns false when candidate is older than baseline", () => {
			expect(isVersionSameOrNewerThan("1.0.0", "2.0.0")).toBe(false)
		})

		it("returns true when candidate equals baseline", () => {
			expect(isVersionSameOrNewerThan("1.2.3", "1.2.3")).toBe(true)
		})

		it("returns ignores patch level when 2-level version candidate equals baseline minor version", () => {
			expect(isVersionSameOrNewerThan("v1.2", "1.2.3")).toBe(true)
		})
	})

	describe("isOlderRelease", () => {
		it("returns true when acknowledgedVersion is null", () => {
			expect(isOlderRelease("1.0.0", null)).toBe(true)
		})

		it("returns false when release version is same as acknowledgedVersion", () => {
			expect(isOlderRelease("1.0.0", "1.0.0")).toBe(false)
		})

		it("returns true when release version is older than acknowledgedVersion", () => {
			expect(isOlderRelease("0.9.0", "1.0.0")).toBe(true)
		})

		it("returns false when release version is newer than acknowledgedVersion", () => {
			expect(isOlderRelease("2.0.0", "1.0.0")).toBe(false)
		})
	})
})
