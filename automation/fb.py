"""Print one browser_batch action list that schedules schedule.json[i] to Facebook + Instagram in Meta Business Suite.
Usage: python3 fb.py <i> <ref_of_SNL_file_input> [tabId]"""
import json, sys, os, datetime as dt
H = os.path.dirname(os.path.abspath(__file__))
E = json.load(open(os.path.join(H, 'schedule.json')))
COMPOSER = "https://business.facebook.com/latest/composer?asset_id=1177659488757854"
PATCH = ("if (!window.__snlPatched) { const orig = HTMLInputElement.prototype.click; HTMLInputElement.prototype.click = function () { if (this.type === 'file') { this.id = 'snl-file-input'; this.setAttribute('aria-label', 'SNL file input'); if (!this.isConnected) { document.body.appendChild(this); } return; } return orig.call(this); }; window.__snlPatched = true; } "
         "const b=[...document.querySelectorAll('div[role=button],button')].find(e=>e.innerText && e.innerText.trim()==='Add photo/video'); if(b) b.click(); !!b")
def info(i):
    e = E[i]; d = dt.date.fromisoformat(e['date']); h, m = map(int, e['time'].split(':'))
    pid = e['id']
    if pid == 'VIDEO': raise SystemExit('VIDEO post: use the reels composer (see PLAYBOOK.md)')
    paths = [f'/mnt/user-data/uploads/snl/fb_{pid}_slide_{k}.jpg' for k in range(1, e['slides'] + 1)]
    return dict(date=d.strftime('%m/%d/%Y'), hh=f'{h % 12 or 12:02d}', mm=f'{m:02d}', ap='P' if h >= 12 else 'A', paths=paths, fb=e['fb'])
def opener(tab):
    return [{"name": "navigate", "input": {"url": COMPOSER, "tabId": tab, "force": True}},
            {"name": "computer", "input": {"action": "wait", "duration": 3, "tabId": tab}},
            {"name": "javascript_tool", "input": {"action": "javascript_exec", "tabId": tab, "text": PATCH}},
            {"name": "find", "input": {"query": "SNL file input", "tabId": tab}}]
def batch(i, ref, tab):
    x = info(i)
    dd = dt.datetime.strptime(x['date'], '%m/%d/%Y'); want = dd.strftime('%b ') + str(dd.day) + dd.strftime(', %Y')
    vexp = f"{want}|{int(x['hh'])}|{int(x['mm'])}|{x['ap']}M"
    prep = ("await new Promise(r=>setTimeout(r,1500)); const ed=document.querySelector('[contenteditable=true]'); ed.focus(); const dt=new DataTransfer(); "
            f"dt.setData('text/plain', {json.dumps(x['fb'], ensure_ascii=False)}); ed.dispatchEvent(new ClipboardEvent('paste',{{clipboardData:dt,bubbles:true,cancelable:true}})); await new Promise(r=>setTimeout(r,500)); "
            "const lab=[...document.querySelectorAll('*')].find(e=>e.childElementCount===0 && e.textContent.trim()==='Set date and time'); let sw=null,n=lab; for(let i=0;i<6&&n&&!sw;i++){n=n.parentElement; sw=n&&n.querySelector('input[role=switch],input[type=checkbox]');} if(!sw.checked) sw.click(); await new Promise(r=>setTimeout(r,800)); "
            "window.__T=[...document.querySelectorAll('input')].filter(i=>i.placeholder==='mm/dd/yyyy'||['hours','minutes','meridiem'].includes(i.getAttribute('aria-label'))); __T[0].scrollIntoView({block:'center'}); __T[0].focus(); document.activeElement===__T[0]")
    tk = f"Tab {' '.join(x['hh'])} Tab {' '.join(x['mm'])} Tab {x['ap'].lower()} Tab"
    verify = ("const v=__T.map(i=>i.value||i.getAttribute('aria-valuetext')||i.getAttribute('aria-valuenow')); const nmedia=(document.body.innerText.match(/\\d+ x \\d+/g)||[]).length; const cap=document.querySelector('[contenteditable=true]').innerText.length; "
              f"const ok = nmedia>={len(x['paths'])} && cap>20 && v.join('|')==='{vexp}|{vexp}'; if(ok){{const b=[...document.querySelectorAll('div[role=button],button')].filter(e=>e.innerText && e.innerText.trim()==='Schedule'); b[b.length-1].click();}} JSON.stringify({{i:{i}, ok, v:v.join('|'), nmedia, cap}})")
    done = "JSON.stringify({scheduled: document.body.innerText.includes('Your post is scheduled')})"
    return [
        {"name": "file_upload", "input": {"paths": x["paths"], "ref": ref, "tabId": tab}},
        {"name": "javascript_tool", "input": {"action": "javascript_exec", "tabId": tab, "text": prep}},
        {"name": "computer", "input": {"action": "key", "text": "ctrl+a", "tabId": tab}},
        {"name": "computer", "input": {"action": "type", "text": x["date"], "tabId": tab}},
        {"name": "computer", "input": {"action": "key", "text": tk + " ctrl+a", "tabId": tab}},
        {"name": "computer", "input": {"action": "type", "text": x["date"], "tabId": tab}},
        {"name": "computer", "input": {"action": "key", "text": tk, "tabId": tab}},
        {"name": "javascript_tool", "input": {"action": "javascript_exec", "tabId": tab, "text": verify}},
        {"name": "computer", "input": {"action": "wait", "duration": 9, "tabId": tab}},
        {"name": "javascript_tool", "input": {"action": "javascript_exec", "tabId": tab, "text": done}},
    ] + opener(tab)
if __name__ == "__main__":
    tab = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    if sys.argv[1] == 'open': print(json.dumps(opener(tab))); raise SystemExit
    print(json.dumps(batch(int(sys.argv[1]), sys.argv[2], tab), ensure_ascii=False))
