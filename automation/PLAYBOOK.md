# Snap&Learn rolling scheduler: playbook

**Goal:** Snap&Learn posts 3 times a day (07:00, 13:00 and 19:00 SAST) from 27 Oct 2026 to 1 Jan 2027, on two channels:
- Facebook + Instagram, through Meta Business Suite
- TikTok, through TikTok Studio

The full plan is in `schedule.json`. Each entry is indexed by `i` and has these fields:
- `date`, `time` (SAST)
- `id` (post id; `VIDEO` = Video 2)
- `aud`
- `slides`
- `fb` (Facebook/Instagram caption)
- `tk` (TikTok caption)

Neither platform accepts the whole plan up front:
- **Meta Business Suite** only schedules about 29 days ahead. The first time it refused was 25 Nov 19:00 when tried on 27 Oct.
- **TikTok** shows "You can only schedule up to 30 posts." once 30 posts are in its queue.

So this job runs every day and tops up both queues. Never post anything immediately. Always use **Schedule**.

## 0. Setup (every run)
1. Get this repo into the workspace if it isn't there yet:
   ```
   git clone https://github.com/trp999wrld-ops/snaptolearn-media /home/claude/snaptolearn-media
   ```
   If the clone fails, attach the repo with `add_repo` (owner `trp999wrld-ops`, repo `snaptolearn-media`) and clone again.
2. Run `bash automation/setup.sh`. It copies the images to `/mnt/user-data/uploads/snl/` as `fb_<id>_slide_<k>.jpg` and `tk_<id>_story_<k>.jpg`, plus `video2.mp4`. Chrome `file_upload` only accepts files from that folder.
3. Load the Claude in Chrome tools in one ToolSearch call. Include `browser_batch`, `navigate`, `javascript_tool`, `find`, `file_upload`, `computer`, `get_page_text`, `tabs_context_mcp` and `tabs_create_mcp`.
4. Call `tabs_context_mcp`, then open two new tabs.
   - **No response from Chrome:** report "Trap's computer/Chrome is off — nothing scheduled today" and stop.
   - **Facebook or TikTok shows a login page:** report it and stop. Never enter passwords.

## 1. Facebook + Instagram (Meta Business Suite)
1. Open `https://business.facebook.com/latest/posts/scheduled_posts?asset_id=1177659488757854` and read it with `get_page_text`.
   - The list is newest first.
   - Each post appears twice: "Snap2Learn" is Facebook and "snap2learn" is Instagram.
   - Note the latest scheduled date and time.
   - If the javascript tool says "BLOCKED: Cookie/query string data", use `get_page_text` instead.
2. Run `python3 automation/plan.py fb`. It lists the posts inside Meta's window. Schedule every listed post that comes after the latest one already scheduled, in order.
   - If the list shows a gap, schedule the missing posts too. Match by caption text.
3. Schedule each post with the composer:
   - Start with `python3 automation/fb.py open 0 <tab>` and run its actions. They open the composer, patch the file picker and `find` the input. Note the ref it returns, usually `ref_199` or `ref_205`.
   - Then for each post, run the actions printed by `python3 automation/fb.py <i> <ref> <tab>` as a single `browser_batch`.
   - The verify step must print `"ok":true` and the done step `"scheduled":true`.
   - Each batch ends by reopening the composer and running `find`. Use the ref it returns for the next post.
   - If `"ok":false` with a date of `Oct…`, or `"scheduled":false`, the post is beyond Meta's window. Stop the Facebook part.
   - Do at most 3 posts per `browser_batch` call. Bigger batches time out.
4. **VIDEO posts (i = 110 and 141): use the reels composer instead.**
   1. Open `https://business.facebook.com/latest/reels_composer?asset_id=1177659488757854`.
   2. Run the same click patch (the PATCH string in `fb.py`), but click the button whose text is "Add Video".
   3. `find` "SNL file input" and `file_upload` `/mnt/user-data/uploads/snl/video2.mp4`. Wait about 20 s.
   4. Paste the `fb` caption into the contenteditable using the same ClipboardEvent paste as `fb.py`.
   5. Click **Next** twice, then choose the **Schedule** option.
   6. Set the date and time. Facebook's fields are `__T[0..3]` and Instagram's are `__T[4..7]`; fill each set separately as in `fb.py`.
   7. Click the last **Schedule** button and check for "scheduled".
5. Finally, re-read the scheduled list and confirm that each new post shows twice (Facebook + Instagram) at the right time.

### Meta link limit (found 28 Oct 2026)
Without a paid Meta One subscription, the Page can only add links to 2 posts per month. Once that's used up, the composer greys out **Schedule** for any caption containing `snaptolearn.co.za`; hovering the button shows "Delete your link to finish posting". If you see that, stop the Facebook part. Do not edit captions on your own; follow whatever Trap decided (see the latest status note) and report it.

## 2. TikTok (TikTok Studio)
1. Open `https://www.tiktok.com/tiktokstudio/content` and read it.
   - Scheduled posts show the hashtag line plus a future date such as "13 Nov, 1:00 pm".
   - Note the latest scheduled date.
2. Install the helper once per run: run the action printed by `python3 automation/tk.py install 0 <tab>` while the tab is on tiktok.com. It stores the helper in localStorage.
3. Run `python3 automation/tk.py open 0 <tab>`. It opens the photo uploader, clicks "Discard" on the unsaved-draft prompt, and finds the file input (usually `ref_99`, `ref_97` or `ref_90`).
4. Run `python3 automation/plan.py tk`. Take the posts after the latest one already scheduled, in order, and for each run the actions from `python3 automation/tk.py <i> <ref> <tab>`.
   - The schedule step must return `"ok":true` and `"done":true`.
   - Each batch ends by reopening the uploader and running `find`. Use the ref it returns next time.
   - If the result is `"done":false` or `cap30:true`, TikTok's 30-post cap has been reached. Stop the TikTok part; it is not an error.
   - Do at most 3 posts per `browser_batch` call.
5. **VIDEO posts (i = 23, 110 and 141):**
   - Get the video file input by running the actions from `python3 automation/tk.py vopen 0 <tab>`.
   - Then run `python3 automation/tk.py <i> <video_ref> <tab>`. It uploads `video2.mp4`, replaces the description with the caption and schedules it.
   - Afterwards, use `tk.py open` to get back to photos.
   - **i = 23 (4 Nov 13:00, Video 2) has not been scheduled on TikTok yet.** The 30-post cap blocked it on 27 Oct. Schedule it as soon as the cap allows; the post is still due if its time has not passed.
6. Re-read the content list and confirm the new posts appear.

## 3. Report (short, readable on a phone)
- How many posts were added to Facebook + Instagram, and the latest date now queued.
- How many posts were added to TikTok, and the latest date now queued.
- Anything missing or failed, in plain words. Examples: computer off, logged out, a post that didn't verify.
- After the 1 Jan 2027 posts are all scheduled, say the plan is complete and that the next batch (January 2027) needs planning.

## Rules
- Use only the captions and images from this plan. Do not invent or rewrite content.
- Never delete posts. Never post immediately. Never enter passwords.
- If a step keeps failing after 2 tries, stop that platform and report it rather than looping.
