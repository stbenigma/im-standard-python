import unittest
from pathlib import Path
from INTERFACES.MIRO import MiroSync,boards,frames

class MyTestCase(unittest.TestCase):
    def test_boards(self):

        bds= boards(token="eyJtaXJvLm9yaWdpbiI6ImV1MDEifQ_oguutE_A_bVt33wmcSKanxRpoZE",
                    filter="Miro API")
        bds.sort(key=lambda x:x["name"])
        print("\n".join([f'{b["id"]}\t{b["name"]}' for b in bds]))

    def test_frames(self):

        frms= frames(token="eyJtaXJvLm9yaWdpbiI6ImV1MDEifQ_oguutE_A_bVt33wmcSKanxRpoZE",
                     boardid="uXjVMx6gvuQ=",
                    filter="^.*")
        frms.sort(key=lambda x:x["name"])
        print("\n".join([f'{b["id"]}\t{b["name"]}\t{str(round(b["width"],1))} x {str(round(b["height"],1))}' for b in frms]))

    def test_pull(self):
        miro = MiroSync(token="eyJtaXJvLm9yaWdpbiI6ImV1MDEifQ_oguutE_A_bVt33wmcSKanxRpoZE")
        miro.pull(frame_id=3458764666214036549, #Geschäfts... 3458764661002109900, #System Land 3458764661076547237,
                  board_id="uXjVMx6gvuQ=",
                  out_file=str(Path.home()/"Downloads" /"pulltest.json"))

    def test_push(self):
        miro = MiroSync(token="eyJtaXJvLm9yaWdpbiI6ImV1MDEifQ_oguutE_A_bVt33wmcSKanxRpoZE")
        miro.push(board_id="uXjVMx6gvuQ=",
                  json_file=str(Path.home()/"Downloads" /"pulltest.json"),
                  withexamples=False)

    def test_texts(self):
        miro = MiroSync(token="eyJtaXJvLm9yaWdpbiI6ImV1MDEifQ_oguutE_A_bVt33wmcSKanxRpoZE")
        texts=miro.get_texts(frame_id=3458764666214036549, #Geschäfts... 3458764661002109900, #System Land 3458764661076547237,
                  board_id="uXjVMx6gvuQ=")
        print (texts)
        return

    def test_groups(self):
        miro = MiroSync(token="eyJtaXJvLm9yaWdpbiI6ImV1MDEifQ_oguutE_A_bVt33wmcSKanxRpoZE")
        texts=miro.get_texts(frame_id=3458764666214036549, #Geschäfts... 3458764661002109900, #System Land 3458764661076547237,
                  board_id="uXjVMx6gvuQ=")
        shapes=miro.get_shapes(frame_id=3458764666214036549,
                            board_id="uXjVMx6gvuQ=")
        ids={s["id"] for s in shapes}.union({t["id"] for t in texts})
        groups=miro.get_groups(board_id="uXjVMx6gvuQ=",itemlist=ids)
        example=miro.get_item_text(item_id='3458764666214036571',groups=groups,texts=texts)
        return

if __name__ == '__main__':
    unittest.main()
