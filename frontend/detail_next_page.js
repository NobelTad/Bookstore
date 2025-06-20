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
        <h1 className="title">{data.name}</h1>
        <p className="desc">{data.description}</p>

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
        /* Base card size (30% bigger than before) */
        .card {
          display: flex;
          max-width: 936px; /* 720 * 1.3 */
          height: 364px; /* 280 * 1.3 */
          margin: 60px 0 60px 0; /* no auto to stick left */
          background: #ffffff;
          border-radius: 18px;
          box-shadow: 0 15px 40px rgba(0, 0, 0, 0.1);
          overflow: hidden;
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          align-items: center; /* vertical center */
          padding-right: 40px;
          padding-left: 0; /* flush left */
        }

        .poster-wrapper {
          flex: 0 0 286px; /* keep 286px width for image container */
          height: 364px; /* match card height */
          background: #f7f8fa;
          display: flex;
          align-items: center;
          justify-content: center;
          overflow: hidden;
          border-radius: 18px 0 0 18px; /* rounded left corners */
          box-shadow: 0 5px 15px rgba(0, 0, 0, 0.12);
          margin-right: 40px;
          margin-left: 0;
        }

        .poster {
          width: 234px; /* 180 * 1.3 */
          height: 338px; /* 260 * 1.3 */
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

        .title {
          font-size: 2.86rem; /* 2.2 * 1.3 */
          font-weight: 700;
          color: #222;
          margin-bottom: 20px;
          letter-spacing: 0.03em;
          user-select: text;
        }

        .desc {
          font-size: 1.3rem; /* 1 * 1.3 */
          line-height: 1.6;
          color: #555;
          user-select: text;
          overflow: hidden;
          max-height: 182px; /* 140 * 1.3 */
          text-overflow: ellipsis;
          white-space: pre-wrap;
          margin-bottom: 91px; /* 70 * 1.3 space for button */
        }

        .download-btn {
          position: absolute;
          bottom: 0;
          right: 0;
          padding: 16px 36px; /* 12x1.3 and 28x1.3 */
          background: #0070f3;
          color: white;
          font-weight: 600;
          border-radius: 0 0 18px 0;
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
          .title {
            font-size: 2rem;
            margin-bottom: 16px;
          }
          .desc {
            margin-bottom: 70px;
            font-size: 1.2rem;
            max-height: none;
          }
          .download-btn {
            bottom: 0;
            right: 0;
            padding: 14px 30px;
            font-size: 1.1rem;
            border-radius: 0 0 12px 0;
          }
        }
      `}</style>
    </div>
  );
}
