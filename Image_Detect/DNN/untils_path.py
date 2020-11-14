import os

image_types = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff")


def list_images(basePath, contains=None):
    # 返回有效的圖片路徑
    return list_files(basePath, validExts=image_types, contains=contains)


def list_files(basePath, validExts=None, contains=None):
    # 尋找圖片數據目錄，生成美張圖片的路徑
    for (rootDir, dirNames, filenames) in os.walk(basePath):
        # 循還尋找當前目錄中的文件名
        for filename in filenames:
            # if the contains string is not none and the filename does not contain
            # the supplied string, then ignore the file
            if contains is not None and filename.find(contains) == -1:
                continue

            # 通過確定.的位置，从而确定当前文件的文件擴展名
            ext = filename[filename.rfind("."):].lower()

            # 检查文件是否為圖像，是否應進行處理
            if validExts is None or ext.endswith(validExts):
                # 構造圖像路徑
                imagePath = os.path.join(rootDir, filename)
                yield imagePath