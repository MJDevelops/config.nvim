local M = {}

---@param file string
function exists(file)
	local ok, err, code = os.rename(file, file)
	if not ok then
		if code == 13 then
			return true
		end
	end
	return ok, err
end

---@param path string
function M.isdir(path)
	return exists(path .. "/")
end

return M
