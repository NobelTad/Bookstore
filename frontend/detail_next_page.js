'use client';

import { useParams } from 'next/navigation';
import { useEffect, useState } from 'react';

export default function Details() {
  const { no } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!no) return;
    fetch(`http://localhost:5000/detail/${no}`)
      .then(res => res.json())
      .then(json => {
        setData(json);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, [no]);

  if (loading) return <div className="loading">Loading...</div>;
  if (!data || data.error) return <div className="error">No data found</div>;

  return (
    <div className="card">
      <div className="poster-wrapper">
        <img
          src={data.poster || '/default-book-cover.jpg'}
          alt={data.name || 'Cover'}
          className="poster"
          loading="lazy"
        />
      </div>
      <div className="content">
        <div className="title-desc-wrapper">
          <h1 className="title">{data.name}</h1>
          <div className="vertical-line" />
          <p className="desc">{data.description}</p>
        </div>

        <a
          href={data.url}
          download
          className="download-btn"
          target="_blank"
          rel="noopener noreferrer"
        >
          ⬇ Download PDF
        </a>
      </div>

      <style jsx>{`
        .card {
          display: flex;
          max-width: 936px;
          height: 364px;
          margin: 60px 0 60px 0;
          background: #ffffff;
          border-radius: 18px;
          box-shadow: 0 15px 40px rgba(0, 0, 0, 0.1);
          overflow: hidden;
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          align-items: center;
          padding-right: 40px;
          padding-left: 0;
        }

        .poster-wrapper {
          flex: 0 0 286px;
          height: 364px;
          background: #f7f8fa;
          display: flex;
          align-items: center;
          justify-content: center;
          overflow: hidden;
          border-radius: 18px 0 0 18px;
          box-shadow: 0 5px 15px rgba(0, 0, 0, 0.12);
          margin-right: 40px;
          margin-left: 0;
        }

        .poster {
          width: 234px;
          height: 338px;
          object-fit: cover;
          border-radius: 12px;
          transition: transform 0.3s ease;
        }

        .poster:hover {
          transform: scale(1.05);
        }

        .content {
          flex: 1;
          display: flex;
          flex-direction: column;
          justify-content: center;
          align-items: flex-start;
          position: relative;
          color: #1e1e1e;
          max-height: 364px;
          overflow: hidden;
          padding-right: 0;
        }

        .title-desc-wrapper {
          display: flex;
          align-items: center;
          gap: 20px; /* space between title, line and description */
          max-height: 280px;
          overflow: hidden;
        }

        .title {
          font-size: 2.86rem;
          font-weight: 700;
          color: #222;
          margin: 0;
          letter-spacing: 0.03em;
          user-select: text;
          white-space: nowrap;
          flex-shrink: 0;
          max-width: 45%; /* prevent title from overflowing */
          overflow: hidden;
          text-overflow: ellipsis;
        }

        .vertical-line {
          width: 1px;
          height: 60px;
          background: #ccc;
          border-radius: 1px;
          flex-shrink: 0;
        }

        .desc {
          font-size: 1.3rem;
          line-height: 1.6;
          color: #555;
          user-select: text;
          overflow: hidden;
          max-height: 140px;
          text-overflow: ellipsis;
          white-space: pre-wrap;
          margin: 0;
          flex-grow: 1;
        }

        .download-btn {
          position: absolute;
          bottom: 0;
          right: 0;
          padding: 16px 36px;
          background: #0070f3;
          color: white;
          font-weight: 600;
          border-radius: 50px; /* full pill shape */
          text-decoration: none;
          font-size: 1.3rem;
          box-shadow: 0 8px 20px rgba(0, 112, 243, 0.4);
          transition: background-color 0.3s ease;
          user-select: none;
          cursor: pointer;
        }

        .download-btn:hover {
          background: #005bb5;
          box-shadow: 0 12px 30px rgba(0, 91, 181, 0.6);
        }

        .loading,
        .error {
          max-width: 780px;
          margin: 160px auto;
          font-size: 2.08rem;
          text-align: center;
          color: #666;
          font-weight: 600;
          user-select: none;
        }

        /* Responsive */
        @media (max-width: 600px) {
          .card {
            flex-direction: column;
            max-width: 90vw;
            height: auto;
            padding: 20px;
            margin-left: 0;
          }
          .poster-wrapper {
            margin-right: 0;
            width: 100%;
            height: auto;
            border-radius: 18px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.12);
          }
          .poster {
            width: auto;
            max-height: 338px;
            border-radius: 12px;
            transform: none !important;
            display: block;
            margin: 0 auto;
          }
          .content {
            max-height: none;
            padding: 20px 0 50px;
            position: relative;
            align-items: flex-start;
          }
          .title-desc-wrapper {
            flex-direction: column;
            gap: 12px;
          }
          .title {
            max-width: 100%;
            font-size: 2rem;
            white-space: normal;
          }
          .vertical-line {
            display: none;
          }
          .desc {
            max-height: none;
            font-size: 1.1rem;
          }
          .download-btn {
            bottom: 0;
            right: 0;
            padding: 14px 30px;
            font-size: 1.1rem;
            border-radius: 50px;
          }
        }
      `}</style>
    </div>
  );
}
