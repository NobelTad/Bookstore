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
        <img src={data.poster} alt="Poster" className="poster" />
      </div>
      <div className="content">
        <h1 className="title">{data.name}</h1>
        <p className="desc">{data.description}</p>
        <a href={data.url} download className="download-btn">⬇ Download PDF</a>
      </div>

      <style jsx>{`
        .card {
          display: flex;
          max-width: 100vw;
          height: 450px; /* fixed height */
          margin: 40px auto;
          background: #fff;
          border-radius: 16px;
          box-shadow: 0 10px 25px rgba(0,0,0,0.1);
          overflow: hidden;
          font-family: Arial, sans-serif;
        }
        .poster-wrapper {
          flex: 0 0 45%;
          overflow: hidden;
        }
        .poster {
          width: 100%;
          height: 100%;
          object-fit: cover;
          display: block;
        }
        .content {
          flex: 1;
          padding: 30px 40px;
          display: flex;
          flex-direction: column;
          justify-content: center;
        }
        .title {
          font-size: 2.5rem;
          margin-bottom: 20px;
          color: #222;
        }
        .desc {
          font-size: 1.2rem;
          color: #555;
          flex-grow: 1;
          margin-bottom: 30px;
        }
        .download-btn {
          align-self: flex-start;
          padding: 14px 28px;
          background: #0070f3;
          color: white;
          border-radius: 12px;
          text-decoration: none;
          font-weight: 600;
          font-size: 1.1rem;
          transition: background 0.3s;
        }
        .download-btn:hover {
          background: #0059c1;
        }
        .loading,
        .error {
          text-align: center;
          font-size: 1.5rem;
          margin-top: 3rem;
        }

        /* Responsive for smaller screens */
        @media (max-width: 768px) {
          .card {
            flex-direction: column;
            height: auto;
          }
          .poster-wrapper {
            flex: none;
            height: 300px;
          }
          .poster {
            height: 100%;
          }
          .content {
            padding: 20px;
          }
        }
      `}</style>
    </div>
  );
}
