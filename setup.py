from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='industrial-asset-monitoring',
    version='1.0.0',
    author='Ganesh',
    author_email='ganesh46905ai-cmd@example.com',
    description='AI-Driven Real-Time Industrial Asset Monitoring using Deep Learning',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ganesh46905ai-cmd/Ganesh',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Manufacturing',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.9',
    install_requires=[
        'tensorflow>=2.13.0',
        'torch>=2.0.0',
        'scikit-learn>=1.3.0',
        'pandas>=2.0.0',
        'flask>=2.3.0',
        'paho-mqtt>=1.6.0',
        'redis>=5.0.0',
        'sqlalchemy>=2.0.0',
        'pyyaml>=6.0',
        'pydantic>=2.1.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.4.0',
            'pytest-cov>=4.1.0',
            'black>=23.7.0',
            'flake8>=6.1.0',
            'mypy>=1.5.0',
        ],
        'monitoring': [
            'prometheus-client>=0.17.0',
            'elasticsearch>=8.9.0',
        ],
        'edge': [
            'tflite-runtime>=2.13.0',
            'onnxruntime>=1.16.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'asset-monitoring=main:main',
        ],
    },
)
