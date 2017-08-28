# ImporterForTrakt

Tool to import a CSV file containing watched show episodes and movies to Trakt.
The tool assumes the same format as the exported CSV from Trakt (requires VIP), however so long as the `watched_at` and `episode_trakt_id` headers for episodes and `watched_at` and `trakt_id` headers for movies are present, it _should_ work.
Duplicate entries are not checked for - if the watch history already exists for an episode/movie, a duplicate entry will be added. It is recommended that you either start with a clean watch history, or import a CSV that has no duplicates in.

Please read the Support / Warnings section before using this tool.

Although this was hacked up breifly for my own personal usage, I hope it may be useful to you.

The tool heavily uses [fuzeman's trakt.py API library](https://github.com/fuzeman/trakt.py). I would like to express my thanks to him for creating this API library - without it this tool would have taken much longer to create!

# Usage

1. Install tool requirements;
`pip install -r requirements.txt`

2. Run tool, using the `--file` argument to specify 
`python importer.py --file history.csv`

3. When prompted, navigate in your browser to the URL and input the PIN in to the tool. This only needs to be performed once, after which the login is cached until it expires.

4. Watch the output of the tool. Logging is on `INFO` level by default, you may need to increase it to `DEBUG` if you encounter any issues.

# Support / Warnings

No formal support is available for the tool, best effort support is available via the Github issue tracker - please be as detailed as possible about any issues you run in to. I wrote this tool quickly to fix my Trakt history after a different API tool errornously removed some entries. Only very limited testing has been performed and only for my own data. It may work for you, it may not. Before running it, please ensure you have fully backed up your Trakt data using Trakt's export functionality (requires VIP). However, as this tool uses an exported Trakt CSV you *should* already have a backup.

The tool will take some time to run, approximately 2-3 seconds per entry in your CSV file, as the tool does not batch additions.

Particular attention is drawn to the licence, specifically;

>>>
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
>>>