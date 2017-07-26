def copy_file(glob, dst_dir, src_dir=Path('.')) :
	for src_pth in src_dir.glob(glob) :
		dst_pth = dst_dir / src_pth.relative_to(src_dir)
		if src_pth.is_file() and not dst_pth.parent.exists() :
			dst_pth.parent.mkdir(parents=True)
		shutil.copy(str(src_pth), str(dst_pth))
