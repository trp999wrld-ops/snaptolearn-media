"""Print one browser_batch action list that schedules schedule.json[i] as a TikTok photo post.
Usage: python3 tk.py <i> <ref_of_Select_photos_input> <tabId>   |   python3 tk.py open 0 <tabId>   |   python3 tk.py install 0 <tabId>"""
import json, sys, os
H = os.path.dirname(os.path.abspath(__file__))
E = json.load(open(os.path.join(H, 'schedule.json'))); D = json.load(open(os.path.join(H, 'tkdata.json')))
UP = "https://www.tiktok.com/tiktokstudio/upload?tab=photo"
DISCARD = "let r=false; for(let k=0;k<16;k++){ const b=[...document.querySelectorAll('button')].find(e=>e.innerText.trim()==='Discard'); if(b){b.click(); r=true; break;} await new Promise(x=>setTimeout(x,500)); } await new Promise(x=>setTimeout(x,800)); r"
def opener(tab):
    return [{"name": "navigate", "input": {"url": UP, "tabId": tab, "force": True}},
            {"name": "javascript_tool", "input": {"action": "javascript_exec", "tabId": tab, "text": DISCARD}},
            {"name": "find", "input": {"query": "Select photos file input", "tabId": tab}}]
def post(i, ref, tab):
    e = E[i]; pid = e['id']
    if pid == 'VIDEO': return video(i, ref, tab)
    p = D[str(i)]; tk = e['tk']; k = tk.find(' #'); tags = tk[k + 1:].strip()
    paths = [f"/mnt/user-data/uploads/snl/tk_{pid}_story_{n}.jpg" for n in range(1, e['slides'] + 1)]
    q = {k: p[k] for k in ('t', 'd', 'hdr', 'day')}
    return [
        {"name": "file_upload", "input": {"paths": paths, "ref": ref, "tabId": tab}},
        {"name": "computer", "input": {"action": "wait", "duration": 6, "tabId": tab}},
        {"name": "javascript_tool", "input": {"action": "javascript_exec", "tabId": tab, "text": "eval(localStorage.snlH).title({h:%s})" % json.dumps(p['h'], ensure_ascii=False)}},
        {"name": "computer", "input": {"action": "type", "text": tags + " ", "tabId": tab}},
        {"name": "computer", "input": {"action": "key", "text": "Escape", "tabId": tab}},
        {"name": "javascript_tool", "input": {"action": "javascript_exec", "tabId": tab, "text": "await eval(localStorage.snlH).sched(%d,%s)" % (i, json.dumps(q))}},
    ] + opener(tab)
VUP = "https://www.tiktok.com/tiktokstudio/upload"
def vopener(tab):
    return [{"name": "navigate", "input": {"url": VUP, "tabId": tab, "force": True}},
            {"name": "javascript_tool", "input": {"action": "javascript_exec", "tabId": tab, "text": DISCARD}},
            {"name": "find", "input": {"query": "Select videos file input", "tabId": tab}}]
def video(i, ref, tab):
    """ref must be the VIDEO file input (run: tk.py vopen 0 <tab> first). Video 2 caption goes in the description."""
    import datetime as dt
    e = E[i]; MON = ['January','February','March','April','May','June','July','August','September','October','November','December']
    y, mo, d = e['date'].split('-')
    q = {"t": e['time'], "d": e['date'], "hdr": f"{MON[int(mo)-1]} / {y}", "day": int(d)}
    return [
        {"name": "file_upload", "input": {"paths": ["/mnt/user-data/uploads/snl/video2.mp4"], "ref": ref, "tabId": tab}},
        {"name": "computer", "input": {"action": "wait", "duration": 10, "tabId": tab}},
        {"name": "computer", "input": {"action": "wait", "duration": 10, "tabId": tab}},
        {"name": "javascript_tool", "input": {"action": "javascript_exec", "tabId": tab, "text": "eval(localStorage.snlH).desc()"}},
        {"name": "computer", "input": {"action": "type", "text": e['tk'] + " ", "tabId": tab}},
        {"name": "computer", "input": {"action": "key", "text": "Escape", "tabId": tab}},
        {"name": "javascript_tool", "input": {"action": "javascript_exec", "tabId": tab, "text": "await eval(localStorage.snlH).sched(%d,%s)" % (i, json.dumps(q))}},
    ] + opener(tab)
if __name__ == "__main__":
    i, ref, tab = sys.argv[1], sys.argv[2], int(sys.argv[3])
    if i == 'open': print(json.dumps(opener(tab)))
    elif i == 'vopen': print(json.dumps(vopener(tab)))
    elif i == 'install': print(json.dumps([{"name": "javascript_tool", "input": {"action": "javascript_exec", "tabId": tab, "text": "localStorage.snlH=" + json.dumps(open(os.path.join(H, 'tkhelper.js')).read()) + "; localStorage.snlH.length"}}]))
    else: print(json.dumps(post(int(i), ref, tab), ensure_ascii=False))
