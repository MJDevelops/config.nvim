local osname = require("joel.utils.getOS").getName()
local isdir = require("joel.utils.path").isdir

if not isdir("~/.cargo") then
	if not osname == "Windows" then
		local cmd = vim.system({
			"curl",
			"--proto",
			"'=https'",
			"--tlsv1.2",
			"-sSf",
			"https://sh.rustup.rs",
			"|",
			"sh",
			"-s",
			"--",
			"-y",
		}, { text = true }):wait()
	end
end
