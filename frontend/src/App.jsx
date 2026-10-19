
import { useEffect, useState } from "react";
import {
  Search, Star, GitFork, GitCommit,
  BookOpen, Code2, ExternalLink, ArrowUpRight,
  Activity, LoaderCircle
} from "lucide-react";
import "./App.css";

const colors = [
  "#a78bfa", "#38bdf8", "#34d399",
  "#fbbf24", "#fb7185", "#818cf8", "#f472b6"
];

function StatCard({ icon: Icon, label, value, description }) {
  return (
    <div className="stat-card">
      <div className="stat-card-top">
        <div className="stat-icon"><Icon size={20} /></div>
        <ArrowUpRight size={17} className="subtle" />
      </div>
      <h2>{Number(value ?? 0).toLocaleString()}</h2>
      <h3>{label}</h3>
      <p>{description}</p>
    </div>
  );
}

function LanguageChart({ distribution }) {
  const languages = Object.entries(distribution || {})
    .filter(([, count]) => count > 0)
    .sort((a, b) => b[1] - a[1]);

  const total = languages.reduce((sum, [, count]) => sum + count, 0);

  return (
    <section className="panel">
      <div className="panel-heading">
        <div>
          <span className="eyebrow">TECH STACK</span>
          <h2>Language distribution</h2>
        </div>
        <Code2 size={21} className="subtle" />
      </div>

      {total > 0 ? (
        <>
          <div className="language-bar">
            {languages.map(([name, count], i) => (
              <div
                key={name}
                title={`${name}: ${((count / total) * 100).toFixed(1)}%`}
                style={{
                  width: `${(count / total) * 100}%`,
                  background: colors[i % colors.length]
                }}
              />
            ))}
          </div>

          <div className="language-list">
            {languages.slice(0, 7).map(([name, count], i) => (
              <div className="language-row" key={name}>
                <span className="language-name">
                  <span
                    className="language-dot"
                    style={{ background: colors[i % colors.length] }}
                  />
                  {name}
                </span>
                <span>{((count / total) * 100).toFixed(1)}%</span>
              </div>
            ))}
          </div>
          <p className="footnote">
            Based on the primary language of analyzed repositories.
          </p>
        </>
      ) : (
        <p className="empty">No language data available.</p>
      )}
    </section>
  );
}

function RepositoryCard({ title, repo, type, username }) {
  const name = repo?.name || repo?.full_name || null;
  const count = repo?.[type];
  const url = name
    ? `https://github.com/${encodeURIComponent(username)}/${encodeURIComponent(name)}`
    : null;

  return (
    <div className="repo-card">
      <div className="repo-icon">
        {type === "stars" ? <Star size={20} /> : <GitFork size={20} />}
      </div>
      <div className="repo-details">
        <span className="eyebrow">{title}</span>
        <h3>{name || "Not available"}</h3>
        <p>
          {count == null
            ? "Repository highlight"
            : `${count.toLocaleString()} ${type}`}
        </p>
      </div>
      {url && (
        <a href={url} target="_blank" rel="noreferrer">
          <ExternalLink size={18} />
        </a>
      )}
    </div>
  );
}

export default function App() {
  const [input, setInput] = useState("");
  const [username, setUsername] = useState("");
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!username) return;
    const controller = new AbortController();

    async function loadStats() {
      setLoading(true);
      setError("");
      setStats(null);

      try {
        const response = await fetch(
          `/stats/${encodeURIComponent(username)}`,
          { signal: controller.signal }
        );

        if (!response.ok) {
          if (response.status === 404) {
            throw new Error("GitHub user not found. Try another username.");
          }
          throw new Error(`Unable to fetch statistics (HTTP ${response.status}).`);
        }

        const data = await response.json();
        if (!controller.signal.aborted) setStats(data);
      } catch (err) {
        if (!controller.signal.aborted) {
          setError(err.message || "Something went wrong.");
        }
      } finally {
        if (!controller.signal.aborted) setLoading(false);
      }
    }

    loadStats();
    return () => controller.abort();
  }, [username]);

  function handleSearch(event) {
    event.preventDefault();
    const value = input.trim();

    if (!value) {
      setError("Please enter a GitHub username.");
      return;
    }

    if (!/^[a-zA-Z0-9-]{1,39}$/.test(value)) {
      setError("Please enter a valid GitHub username.");
      return;
    }

    if (value === username) {
      setError("");
      return;
    }

    setUsername(value);
  }

  return (
    <div className="app">
      <header className="navbar">
        <div className="nav-inner">
          <a className="brand" href="/">
            <span className="brand-icon"><Activity size={22} /></span>
            GitStat<span className="brand-dot">.</span>
          </a>

          <div className="nav-right">
            <span className="nav-label">
              <span className="online-dot" />
              GitHub Analytics
            </span>
            <a
              className="github-link"
              href="https://github.com/varen1512/gitstat"
              target="_blank"
              rel="noreferrer"
            >
              <Code2 size={19} />
              <span>GitHub</span>
              <ArrowUpRight size={15} />
            </a>
          </div>
        </div>
      </header>

      <main className="container">
        <section className="hero">
          <div className="hero-tag">
            <span className="sparkle">✦</span>
            YOUR CODE, VISUALIZED
          </div>

          <h1>
            Understand your
            <br />
            <span className="gradient-text">GitHub footprint.</span>
          </h1>

          <p className="hero-description">
            Turn repositories, commits, and programming languages into
            a clear picture of your developer journey.
          </p>

          <form className="search-form" onSubmit={handleSearch}>
            <Search size={21} className="search-icon" />
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Enter a GitHub username..."
              aria-label="GitHub username"
            />
            <button type="submit" disabled={loading}>
              {loading ? <LoaderCircle size={18} className="spin" /> : "Analyze"}
              {!loading && <ArrowUpRight size={17} />}
            </button>
          </form>

          <p className="search-hint">
            Try <button onClick={() => { setInput("octocat"); setUsername("octocat"); }}>octocat</button>
            <span>·</span>
            <button onClick={() => { setInput("torvalds"); setUsername("torvalds"); }}>torvalds</button>
            <span>·</span>
            <button onClick={() => { setInput("gaearon"); setUsername("gaearon"); }}>gaearon</button>
          </p>
        </section>

        {loading && (
          <div className="loading-state">
            <LoaderCircle size={32} className="spin" />
            <h3>Analyzing @{username}</h3>
            <p>Fetching repositories and calculating activity...</p>
          </div>
        )}

        {error && !loading && (
          <div className="error-state">
            <h3>Something went wrong</h3>
            <p>{error}</p>
          </div>
        )}

        {stats && !loading && !error && (
          <div className="results" key={stats.username}>
            <div className="results-heading">
              <div>
                <span className="eyebrow">DEVELOPER OVERVIEW</span>
                <h2>
                  <span className="at-sign">@</span>{stats.username}
                </h2>
                <p>Public GitHub repository analytics</p>
              </div>
              <a
                className="profile-link"
                href={`https://github.com/${encodeURIComponent(stats.username)}`}
                target="_blank"
                rel="noreferrer"
              >
                View Profile <ExternalLink size={16} />
              </a>
            </div>

            <div className="stats-grid">
              <StatCard
                icon={BookOpen}
                label="Repositories"
                value={stats.total_repositories}
                description="Analyzed repositories"
              />
              <StatCard
                icon={Star}
                label="Total Stars"
                value={stats.total_stars}
                description="Across analyzed repositories"
              />
              <StatCard
                icon={GitFork}
                label="Total Forks"
                value={stats.total_forks}
                description="Across analyzed repositories"
              />
              <StatCard
                icon={GitCommit}
                label="Your Commits"
                value={stats.owner_commits_last_52_weeks}
                description="Last 52 weeks"
              />
            </div>

            <div className="details-grid">
              <LanguageChart distribution={stats.language_distribution} />

              <section className="panel activity-panel">
                <div className="panel-heading">
                  <div>
                    <span className="eyebrow">DEVELOPMENT ACTIVITY</span>
                    <h2>Commit overview</h2>
                  </div>
                  <Activity size={21} className="subtle" />
                </div>

                <div className="activity-number">
                  {Number(stats.repo_commits_last_52_weeks ?? 0).toLocaleString()}
                </div>
                <p className="activity-label">Total repository commits · 52 weeks</p>

                <div className="activity-divider" />

                <div className="activity-row">
                  <span>Developer commits</span>
                  <strong>
                    {Number(stats.owner_commits_last_52_weeks ?? 0).toLocaleString()}
                  </strong>
                </div>

                <div className="activity-row">
                  <span>Top language</span>
                  <strong>{stats.top_language || "N/A"}</strong>
                </div>

                <p className="footnote">
                  Activity reflects the repositories included in GitStat's analysis.
                </p>
              </section>
            </div>

            <section className="highlights">
              <div className="section-heading">
                <span className="eyebrow">STANDOUT PROJECTS</span>
                <h2>Repository highlights</h2>
              </div>

              <div className="repo-grid">
                <RepositoryCard
                  title="MOST STARRED"
                  repo={stats.most_starred_repository}
                  type="stars"
                  username={stats.username}
                />
                <RepositoryCard
                  title="MOST FORKED"
                  repo={stats.most_forked_repository}
                  type="forks"
                  username={stats.username}
                />
              </div>
            </section>
          </div>
        )}
      </main>

      <footer className="footer">
        <div className="footer-inner">
          <span>GitStat<span className="brand-dot">.</span> Built with React & FastAPI.</span>
          <span>Made by Varen Kumar</span>
        </div>
      </footer>
    </div>
  );
}
