return {
	"mfussenegger/nvim-lint",
	config = function()
		require("lint").linters_by_ft = {
			lua = { "luac" },
			python = { "pylint" },
			typescript = { "eslint_d" },
			typescriptreact = { "eslint_d" },
			javascript = { "eslint_d" },
			javascriptreact = { "eslint_d" },
			ruby = { "rubocop" },
		}

		vim.api.nvim_create_autocmd({ "BufWritePost", "BufReadPre", "BufEnter" }, {
			callback = function()
				require("lint").try_lint()
			end,
		})
	end,
}
