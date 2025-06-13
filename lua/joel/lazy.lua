local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
local path = require("joel.utils.path")

if not path.isdir(lazypath) then
	vim.system({
		"git",
		"clone",
		"--filter=blob:none",
		"https://github.com/folke/lazy.nvim.git",
		"--branch=stable", -- latest stable release
		lazypath,
	}, { text = true }):wait()
end
vim.opt.rtp:prepend(lazypath)

require("lazy").setup({ { import = "joel.plugins" }, { import = "joel.plugins.lsp" } }, {
	checker = {
		enabled = true,
		notify = false,
	},
	cange_detection = {
		notify = false,
	},
})
