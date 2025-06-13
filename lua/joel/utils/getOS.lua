local M = {}

function M.getName()
	if jit then
		return jit.os
	end

	local fh, _ = assert(io.popen("uname -o 2>/dev/null", "r"))
	local osname

	if fh then
		osname = fh:read()
	end

	return osname or "Windows"
end

return M
